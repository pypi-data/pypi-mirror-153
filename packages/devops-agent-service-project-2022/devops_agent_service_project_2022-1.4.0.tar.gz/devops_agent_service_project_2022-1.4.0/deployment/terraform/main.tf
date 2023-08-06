terraform {
  backend "pg" {
  }
}

provider "heroku" {
}

variable "agent_app_name" {
  description = "Unique name of the agent app"
}

resource "heroku_app" "agent" {
  name   = var.agent_app_name
  region = "eu"
  stack  = "container"
}

resource "heroku_build" "agent" {
  app_id = heroku_app.agent.id

  source {
    path = "agent"
  }
}

resource "heroku_config" "agent" {
  vars = {
    STAGE = "PROD"
  }
}

resource "heroku_app_config_association" "agent" {
  app_id = heroku_app.agent.id

  vars = heroku_config.agent.vars
}

resource "heroku_addon" "database" {
  app_id  = heroku_app.agent.id
  plan = "heroku-postgresql:hobby-dev"
}

output "agent_app_url" {
  value = "https://${heroku_app.agent.name}.herokuapp.com"
}