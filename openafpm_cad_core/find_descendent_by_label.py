__all__ = ['find_descendent_by_label']


def find_descendent_by_label(obj, label: str):
    if obj.Label == label:
        return obj
    elif obj.TypeId == 'App::Link':
        return find_descendent_by_label(obj.LinkedObject, label)
    elif is_link_array(obj):
        return find_descendent_by_label(obj.Base, label)
    elif obj.TypeId == 'App::Part':
        for child in obj.Group:
            grandchild = find_descendent_by_label(child, label)
            if grandchild:
                return grandchild


def is_link_array(obj: object) -> bool:
    return (
        obj.TypeId == 'Part::FeaturePython' and
        hasattr(obj, 'ArrayType')
    )
