import (
	"regexp"
	"strings"
)

func startsWith(needle string, haystack string) bool {
	return strings.HasPrefix(haystack, needle)
}

func contains(needle string, haystrack string) bool {
	return strings.Contains(haystrack, needle)
}

func reMatch(pattern string, text string) bool {
	match, err := regexp.MatchString(pattern, text)
	if err != nil {
		return false
	}
	return match
}

func concatStr(str1 string, str2 string) string {
	return str1 + str2
}
