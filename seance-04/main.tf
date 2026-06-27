terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# 1. Réseau Docker partagé
resource "docker_network" "anfa_net" {
  name = "anfa-network"
}

# 2. Volume persistant pour les données de MinIO
resource "docker_volume" "minio_data" {
  name = "anfa-minio-data-tf"
}

# 3. Image officielle MinIO
resource "docker_image" "minio" {
  name = "minio/minio:latest"
}

# 4. Conteneur MinIO paramétré
resource "docker_container" "minio" {
  name    = var.container_name
  image   = docker_image.minio.image_id
  restart = "unless-stopped"
  
  command = ["server", "/data", "--console-address", ":9001"]

  ports {
    internal = 9000
    external = var.minio_api_port
  }

  ports {
    internal = 9001
    external = var.minio_console_port
  }

  env = [
    "MINIO_ROOT_USER=${var.minio_root_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_root_password}"
  ]

  volumes {
    volume_name    = docker_volume.minio_data.name
    container_path = "/data"
  }

  networks_advanced {
    name = docker_network.anfa_net.name
  }

  # Évite que Terraform ne recrée le conteneur à cause des options de log de Windows
  lifecycle {
    ignore_changes = [log_opts]
  }
}