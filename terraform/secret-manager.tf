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