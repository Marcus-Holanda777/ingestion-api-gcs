resource "google_cloud_scheduler_job" "job" {
  name             = "${var.bucket_name}-job"
  project          = var.project_id
  region           = var.region
  description      = "trabalho api currency"
  schedule         = "0 6 * * *"
  time_zone        = "America/Fortaleza"
  attempt_deadline = "320s"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.Cloud_function.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.bucket_account.email
    }
  }

  depends_on = [
    google_cloudfunctions_function.Cloud_function,
    google_service_account.bucket_account
  ]
}