terraform {
  backend "gcs" {
    bucket      = "cryptoapp-bucket"
    prefix      = "project/gke"
    credentials = "./cred.json"
  }
}

provider "google" {

  credentials = "./cred.json"
  project     = "natural-chiller-347811"
  region      = "europe-west3"
}


resource "google_compute_network" "gke" {
  name                    = "network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "gke" {
  name                     = "subnetwork"
  ip_cidr_range            = "10.2.0.0/16"
  region                   = "europe-west3"
  network                  = google_compute_network.gke.id
  private_ip_google_access = true
  secondary_ip_range {
    range_name    = "services-range"
    ip_cidr_range = "192.168.1.0/24"
  }

  secondary_ip_range {
    range_name    = "pod-ranges"
    ip_cidr_range = "192.168.64.0/22"
  }
}

module "gke" {
  source                     = "terraform-google-modules/kubernetes-engine/google"
  project_id                 = "natural-chiller-347811"
  name                       = "gke-test-1"
  region                     = "europe-west3"
  zones                      = [ "europe-west3-b", "europe-west3-c"]
  network                    = google_compute_network.gke.name
  subnetwork                 = google_compute_subnetwork.gke.name
  ip_range_services          = google_compute_subnetwork.gke.secondary_ip_range.0.range_name
  ip_range_pods              = google_compute_subnetwork.gke.secondary_ip_range.1.range_name
  http_load_balancing        = false
  network_policy             = false
  horizontal_pod_autoscaling = true
  filestore_csi_driver       = false


  node_pools = [
    {
      name               = "default-tnode-pool"
      machine_type       = "e2-medium"
      node_locations     = "europe-west3-b,europe-west3-c"
      min_count          = 1
      max_count          = 6
      local_ssd_count    = 0
      disk_size_gb       = 200
      disk_type          = "pd-standard"
      image_type         = "COS_CONTAINERD"
      enable_gcfs        = false
      auto_repair        = true
      auto_upgrade       = true
      service_account    = "tf-65-702@natural-chiller-347811.iam.gserviceaccount.com"
      preemptible        = false
      remove_default_node_pool = true
      initial_node_count = 1
    },
  ]


  node_pools_oauth_scopes = {
    all = []

    node-pool = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  node_pools_labels = {
    all = {}

    node-pool = {
      node-pool = true
    }
  }

  node_pools_metadata = {
    all = {}

    node-pool = {
      node-pool-metadata-custom-value = "my-node-pool"
    }
  }

  node_pools_taints = {
    all = []

    node-pool = [
      {
        key    = "default-node-pool"
        value  = true
        effect = "PREFER_NO_SCHEDULE"
      },
    ]
  }

  node_pools_tags = {
    all = []

    node-pool = [
      "default-node-pool",
    ]
  }
}
