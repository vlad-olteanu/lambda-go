from ..generic_function import GenericFunction
from typing import Mapping
from dataclasses import dataclass, field
from code_generation.types import expand_type
from utils import tuple_to_list, list_depth

generic_functions: Mapping[str, type] = {}


def generic(cls):
    generic_functions[cls.get_fn_name()] = cls
    return cls


@generic
class TypeCast(GenericFunction):
    @classmethod
    def get_type(cls, argument_types, metadata):
        if len(argument_types) > 1:
            raise Exception(f"{cls.get_fn_name()} expected 1 or 0 arguments")
        if len(argument_types)==0:
            argument_types=[any]
        cast_type = tuple_to_list(metadata["target_type"])
        if len(cast_type)>1:
            cast_type = [cast_type]
        return argument_types + cast_type

    @staticmethod
    def expand(function_type):
        def get_elem_cast(var, src_type, dst_type):
            if src_type is any:
                return f"{var}.({expand_type(dst_type)})"
            return f"{expand_type(dst_type)}({var})"

        src_type = function_type[0]
        dst_type = function_type[1]

        src_type_depth = list_depth(src_type)
        dst_type_depth = list_depth(dst_type)
        
        depth = min([src_type_depth, dst_type_depth])
        # if depth == 0:
        #     return get_elem_cast( "arg0", function_type[0], function_type[1],)
        
        ret_head = [f" func(src0 {expand_type(function_type[0])}) {expand_type(function_type[1])}"+"{"]
        ret_tail = ["}(arg0)"]

        for i in range(depth+1):
            if i < depth:
                ret_head+=[
                    f"dst{i} := {expand_type(dst_type)}"+"{}",
                    f"for _, src{i+1} := range src{i}"+"{"
            #         f"for _, it{i} := range src{i}"+" {"
                ]
                dst_type = dst_type[0]
                src_type = src_type[0]
            else:
                ret_head += [f"dst{i} := {get_elem_cast(f'src{i}', src_type, dst_type)}"]

            if i == 0:
                ret_tail = [f"return dst{i}"] + ret_tail
            else:
                ret_tail = [f"dst{i-1} = append(dst{i-1}, dst{i})", "}"] + ret_tail
            
        return "\n".join(ret_head)+"\n"+"\n".join(ret_tail)


        


"""
// type_cast::[[any]]->[[int]]
func type_cast_1c95f(arg0 [][]interface{}) [][]int {
	arr0 := [][]int{}
	for _, e0 := range arg0 {
		arr1 := []int{}
		for _, e1 := range e0 {
			arr1 = append(arr1, e1.(int))
		}
		arr0 = append(arr0, arr1)
	}
	return arr0
}

// type_cast::[[any]]->[[int]]
func type_cast_1c95f(arg0 [][]interface{}) [][]int {
    return func(e0){
        e1:=[][]int{}

    }(arg0)
	arr0 := [][]int{}
	for _, e0 := range arg0 {
		arr1 := []int{}
		for _, e1 := range e0 {
			arr1 = append(arr1, e1.(int))
		}
		arr0 = append(arr0, arr1)
	}
	return arr0
}

// type_cast::[any]->[[int]]
func type_cast_c119a(arg0 []interface{}) [][]int {
	arr0 := [][]int{}
	for _, e := range arg0 {
		arr0 = append(arr0, e.([]int))
	}
	return arr0
}


// type_cast::[any]->[int]
func type_cast_36e98(arg0 []interface{}) []int {
	arr0 := []int{}
	for _, e := range arg0 {
		arr0 = append(arr0, e.(int))
	}
	return arr0
}
"""