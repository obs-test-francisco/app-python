data "google_client_config" "current" {}

data "google_secret_manager_secret_version" "observe" {
  secret = "provider_observe"
  version = "latest"
  fetch_secret_data = true
}