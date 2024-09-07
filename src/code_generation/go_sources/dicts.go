import "strings"

func dictGetDefault(d map[string]interface{}, jsonPath string, defaultValue interface{}) interface{} {
	if v, ok := d[jsonPath]; ok {
		return v
	}
	return defaultValue
}

func dictGet(d map[string]interface{}, jsonPath string) interface{} {
	return d[jsonPath]
}

func dictDeepGet(d map[string]interface{}, jsonPath string, defaultValue interface{}) interface{} {
	path := strings.Split(jsonPath, ".")
	var e interface{} = d
	var ok bool
	for _, key := range path {
		d, ok = e.(map[string]interface{})
		if !ok {
			return defaultValue
		}
		e, ok = d[key]
		if !ok {
			return defaultValue
		}
	}
	return e
}

func dictDeepSet(d map[string]interface{}, jsonPath string, value interface{}) map[string]interface{} {
	path := strings.Split(jsonPath, ".")
	var d2 map[string]interface{} = d
	// create path up to leaf node
	for _, key := range path[:len(path)-1] {
		e, ok := d2[key]
		if !ok {
			d2[key] = map[string]interface{}{}
			e = d2[key]
		}
		d2, ok = e.(map[string]interface{})
		if !ok {
			return nil
		}
	}
	leafKey := path[len(path)-1]
	d2[leafKey] = value
	return d
}

func dictSet(d map[string]interface{}, jsonPath string, value interface{}) map[string]interface{} {
	d[jsonPath] = value
	return d
}

func dictKeys(d map[string]interface{}) []string {
	var keys []string = []string{}

	for k, v := range d {

		if subdict, ok := v.(map[string]interface{}); ok {
			subkeys := dictKeys(subdict)

			for i, subkey := range subkeys {
				subkeys[i] = k + "." + subkey
			}
			keys = append(keys, subkeys...)
		} else {
			keys = append(keys, k)
		}
	}

	return keys
}
