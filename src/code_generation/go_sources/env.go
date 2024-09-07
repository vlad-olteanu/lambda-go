import "os"

func get_env(key string) string {
	return os.Getenv(key)
}
