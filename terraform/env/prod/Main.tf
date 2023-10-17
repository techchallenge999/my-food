module "prod" {
    source = "../../infra"

    nome_repositorio = "my-food"
    cluster_name = "my-food"
    cluster_version = "1.28"

    username = "master"
    password = "masterPass"
}
