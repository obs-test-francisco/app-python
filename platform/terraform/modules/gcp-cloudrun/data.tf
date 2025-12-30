data "google_client_config" "current" {}

data "google_secret_manager_secret_version" "observe" {
  secret = "provider_observe"
  version = "1"
  fetch_secret_data = true
}