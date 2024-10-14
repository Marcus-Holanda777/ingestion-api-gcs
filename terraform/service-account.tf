resource "google_service_account" "bucket_account" {
  account_id   = "${var.bucket_name}-${var.project_id}"
  display_name = "trabalho api currency"
}

resource "google_service_account_key" "bucket_account_key" {
  service_account_id = google_service_account.bucket_account.name
  public_key_type    = "TYPE_X509_PEM_FILE"
  private_key_type   = "TYPE_GOOGLE_CREDENTIALS_FILE"
}

resource "local_file" "bucket_account_key_file" {
  content  = base64decode(google_service_account_key.bucket_account_key.private_key)
  filename = "${path.module}/service_account_key.json"
}