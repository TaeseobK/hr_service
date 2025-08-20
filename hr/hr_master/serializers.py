from rest_framework import serializers
from .models import *

"""

⚠ Heed This Warning, Successor ⚠

Beneath these lines lies an ancient incantation, woven into the very veins of every serializer that breathes life into this realm. 
Its essence flows unseen through the arteries of our code, binding chaos and order in a fragile truce. 
To alter it without true understanding — and without the blessing of the Elders — is to tear open the gates of ruin. 
Data will twist, APIs will scream, and the system will collapse into a silence more dreadful than death.

Remember, this is no mere function, but a seal of power that holds the balance. 
Break it, and no redemption shall follow. 
If you read this, successor, know this truth: let it remain untouched… or prepare to have your name whispered as a cautionary tale in the dim, 
haunted corners of every developer's gathering.

May God of Knowledge Bless You.



"""

class DynamicModelSerializer(serializers.ModelSerializer):
    """
    Bisa filter 'fields' dan 'exclude' (diambil dari kwargs atau query_params).
    """
    def __init__(self, *args, **kwargs):
        # Ambil context request
        context = kwargs.get('context', {})
        request = context.get('request')

        # Ambil fields & exclude dari kwargs
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Kalau ada query_params, ambil dari sana
        if request:
            qp = request.query_params
            if fields is None and 'fields' in qp:
                fields = [f.strip() for f in qp.get('fields', '').split(',') if f.strip()]
            if exclude is None and 'exclude' in qp:
                exclude = [f.strip() for f in qp.get('exclude', '').split(',') if f.strip()]

        super().__init__(*args, **kwargs)

        # Filter fields
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        # Exclude fields
        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class BaseTreeSerializer(DynamicModelSerializer):
    """
    Dasar serializer pohon:
    - Menyembunyikan 'children' saat render mode parent chain.
    - Menyembunyikan 'parent' saat render mode children tree.
    - Mencegah recursion karena field lawan di-drop SEBELUM to_representation jalan.
    """
    TREE_PARENT_FIELD = 'parent'     # override kalau nama field parent beda
    TREE_CHILDREN_FIELD = 'children' # override kalau related_name beda

    def __init__(self, *args, **kwargs):
        # mode opsional via arg; default ambil dari context
        self.tree_mode = kwargs.pop('tree_mode', None)
        super().__init__(*args, **kwargs)

    def get_fields(self):
        fields = super().get_fields()
        mode = self.tree_mode or self.context.get('_mode')

        if mode == 'parent':
            # Saat berjalan ke atas, jangan ikutkan children
            fields.pop(self.TREE_CHILDREN_FIELD, None)
        elif mode == 'children':
            # Saat berjalan ke bawah, jangan ikutkan parent
            fields.pop(self.TREE_PARENT_FIELD, None)

        return fields


class SmartRecursive(serializers.Serializer):
    """
    Helper rekursif universal:
    - Bisa dipakai di semua serializer turunan BaseTreeSerializer.
    - Tidak wajib passing serializer_class, otomatis ambil dari induknya.
    - Depth guard mencegah infinite recursion.
    """
    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop('mode', None)  # "parent" | "children"
        super().__init__(*args, **kwargs)

    def get_serializer_class(self):
        """
        Cari serializer class induk dengan aman.
        Hindari infinite recursion (jangan ambil SmartRecursive lagi).
        """
        parent = getattr(self, 'parent', None)
        if parent is None:
            return None

        # Ambil serializer induk langsung
        if isinstance(parent, serializers.ListSerializer):
            parent = parent.parent

        if parent and not isinstance(parent, SmartRecursive):
            return parent.__class__

        return None

    def to_representation(self, value):
        serializer_class = self.get_serializer_class()
        if serializer_class is None:
            return {
                'id': getattr(value, 'id', None),
                'name': getattr(value, 'name', None)
            }

        context = dict(self.context or {})
        context['_mode'] = self.mode

        # Ambil max_depth dari query_params jika ada
        if 'request' in context:
            try:
                query_depth = int(context['request'].query_params.get('max_depth', 10))
            except ValueError:
                query_depth = 10
            context['_max_depth'] = query_depth
        else:
            context['_max_depth'] = context.get('_max_depth', 10)

        # Depth guard
        depth = int(context.get('_depth', 0))
        max_depth = int(context['_max_depth'])
        if depth >= max_depth:
            return {
                'id': getattr(value, 'id', None),
                'name': getattr(value, 'name', None)
            }
        context['_depth'] = depth + 1

        kwargs = {'context': context}
        if 'fields' in context and hasattr(serializer_class, 'get_fields'):
            kwargs['fields'] = context['fields']

        return serializer_class(value, **kwargs).data


class CompanySerializer(BaseTreeSerializer):
    children = SmartRecursive(many=True, read_only=True, mode='children')
    parent = SmartRecursive(read_only=True, mode='parent')

    class Meta:
        model = Company
        fields = '__all__'

class UnitSerializer(BaseTreeSerializer) :
    children = SmartRecursive(many=True, read_only=True, mode='children')
    parent = SmartRecursive(read_only=True, mode='parent')

    class Meta:
        model = Unit
        fields = '__all__'

class LevelSerializer(BaseTreeSerializer) :
    children = SmartRecursive(many=True, read_only=True, mode='children')
    parent = SmartRecursive(read_only=True, mode='parent')

    class Meta:
        model = Level
        fields = '__all__'

class EmploymentTypeSerializer(serializers.ModelSerializer) :
    class Meta:
        model = EmploymentType
        fields = '__all__'

class ShiftSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Shift
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer) :
    company = CompanySerializer(many=True, read_only=True)
    class Meta:
        model = Branch
        fields = '__all__'
    
class EmployeeSerializer(BaseTreeSerializer) :
    children = SmartRecursive(many=True, read_only=True, mode='children')
    parent = SmartRecursive(read_only=True, mode='parent')

    unit = UnitSerializer(many=True, read_only=True)
    level = LevelSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    shift = ShiftSerializer(read_only=True)
    employment_type = EmploymentTypeSerializer(read_only=True)

    company = CompanySerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'