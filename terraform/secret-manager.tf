resource "google_secret_manager_secret" "segredo" {
  project   = var.project_id
  secret_id = var.id_secret

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "segredo_version" {
  secret      = google_secret_manager_secret.segredo.id
  secret_data = var.default_key
}

resource "google_secret_manager_secret_iam_member" "segredo_access" {
  secret_id = google_secret_manager_secret.segredo.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.bucket_account.email}"
}

resource "google_secret_manager_secret" "key_account" {
  project   = var.project_id
  secret_id = var.id_secret_json

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "key_account_version" {
  secret      = google_secret_manager_secret.key_account.id
  secret_data = base64decode(google_service_account_key.bucket_account_key.private_key)
}

resource "google_secret_manager_secret_iam_member" "key_account_access" {
  secret_id = google_secret_manager_secret.key_account.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.bucket_account.email}"
}