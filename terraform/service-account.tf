resource "google_service_account" "bucket_account" {
  account_id   = "${var.bucket_name}-${var.project_id}"
  display_name = "trabalho api currency"
}