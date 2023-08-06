#pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import ast
import re

class ParseError(ValueError):
    pass

class StepNotFound(KeyError):
    pass

def class_name_to_sentence(name):
    a = re.compile(r'([A-Z]+)')
    b = re.compile(r'([A-Z][a-z])')
    c = re.compile(r'\W+')
    return c.sub(' ', b.sub(r' \1', a.sub(r' \1', name))).strip()

def is_step(node):
    if not isinstance(node, ast.ClassDef):
        return False
    for base in node.bases:
        if isinstance(base, ast.Name):
            if base.id == 'Step':
                return True
        elif isinstance(base, ast.Attribute):
            if base.attr == 'Step' and base.value.id == 'factory':
                return True

    return False

def find_step_classes(nodes):
    return [node for node in nodes.body if is_step(node)]

def find_step_list(nodes):
    for node in nodes.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if target.id == 'STEPS' and isinstance(node.value, ast.List):
                return node.value
    return None

def find_assign(classdef, name):
    for node in classdef.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return ast.literal_eval(node.value)

    return None
def get_name(classdef):
    assigned_name = find_assign(classdef, 'DisplayName')
    if assigned_name:
        return assigned_name
    return class_name_to_sentence(classdef.name)

def get_description(classdef):
    return find_assign(classdef, 'Description')

def get_image(classdef):
    return find_assign(classdef, 'Image')

def get_link(classdef):
    return find_assign(classdef, 'Link')

def build_output_steps(step_list, step_classes):
    name_map = {cls.name: cls for cls in step_classes}
    output = []
    for elt in step_list.elts:
        try:
            classdef = name_map[elt.id]
        except KeyError:
            raise StepNotFound(elt.id)
        name = get_name(classdef)
        description = get_description(classdef)
        image = get_image(classdef)
        link = get_link(classdef)
        node = {
            'class': classdef.name,
            'name': name,
            'description': description,
            'image': image,
            'link': link,
        }
        output.append(node)
    return output

def parse_code(nodes):
    step_classes = find_step_classes(nodes)
    step_list = find_step_list(nodes)

    if step_list is None:
        raise ParseError('No steps found')

    return build_output_steps(step_list, step_classes)
