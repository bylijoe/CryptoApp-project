# CICD

## Githuh Actions:

* Plataforma de integración y despliegue continuos (CI/DC) que te permite automatizar tu mapa de compilación, pruebas y despliegue. Puedes crear flujos de trabajo y crear y probar cada solicitud de cambios en tu repositorio o desplegar solicitudes de cambios fusionadas a producción.

* Permite ejecutar flujos de trabajo cuando otros eventos suceden en tu repositorio. Por ejemplo, puedes ejecutar un flujo de trabajo para que agregue automáticamente las etiquetas adecuadas cada que alguien cree una propuesta nueva en tu repositorio.

* Proporciona máquinas virtuales Linux, Windows y macOS para que ejecutes tus flujos de trabajo o puedes hospedar tus propios ejecutores auto-hospedados en tu propio centro de datos o infraestructura en la nube.



 ### CI


  * El evento que ejecutara este workflow será que se sollicitara una solicitud de extraccion "PR" o se produzca algun cambio en el directorio correspondiente a nuestra aplicacion /src
  
          on:
            pull_request:
              branches:
                - '*'
              paths: 'src/**'
            push:
              branches:
                - '*'
              paths: 'src/**'
              
 * Los jobs que se emplean en este workflows 
 
    - Primeramente utilizaremos un  **Linter** , el cual es una herramienta que verifica los errores tipográficos, el estilo del codigo y otros errores en el codigo si ejecutarlo realmente. Este proceso se denomina análisi de codigo estático.
    en nuestro caso hemos utilizado [Flake8](https://github.com/marketplace/actions/flake8-annotator), hemos añadido   la **actions/upload-artifact@v2**, la cual nos permitira cargar artefactos de nuestro flujo de trabajo, esto permite compartir datos entre trabajos y almacenarlos( path: reports/flake8/) una vez que se completa un workflows
           
        - **actions/checkout@v2**:  Descarga nuestro codigo  de esta forma verificamos nuestro repositorio para que nuestro flujo de trabajo pueda acceder a él.
        - **actions/setup-python@v2**: configuramos un entrono python que emplearemos en nuestro flujo   
        -  **Lint with flake8**: Instalara y ejecutara flake8 [docs](https://medium.com/swlh/enhancing-code-quality-with-github-actions-67561c6f7063)
        -  **actions/upload-artifact@v2**: Esta actions nos permitira cargar artefactos de nuestro flujo de trabajo, esto permite compartir datos entre trabajos y almacenarlos( path: reports/flake8/) una vez que se completa un workflows
           
                  flake8:
                    name: Code Quality
                    runs-on: ubuntu-latest
                    steps:
                    - name:  Checkout code
                      uses: actions/checkout@v2

                    - name: Set up Python 3.8
                      uses: actions/setup-python@v2
                      with:
                        python-version: 3.8
                    - name: Lint with flake8
                      run: |
                        pip install flake8 flake8-html
                        # stop the build if there are Python syntax errors or undefined names
                        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
                        mkdir -p reports/flake8
                        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=79 --statistics --format=html --htmldir=reports/flake8
                    - name: Archive flake8 coverage results
                      uses: actions/upload-artifact@v2
                      with:
                        name: flake8-coverage-report
                        path: reports/flake8/
                
      - Posteriormente encontramos otro job el cual ejecutara los test unitarios implementados en nuestro codigo, el cual contsa de los sguientes pasos
        que pasaremos a comentar , hemos omitido acciones anteriormente descritas:
        
        - **Install dependencies**: Este steps se encargara de actualizar pip e instalacion de las librerias contenidas en los requerimientos 
        - **Test with pytest**: instala pytest(aunq esta incluido en requeriments.txt) y sus restantes complementos y se ejecutan los test mostrandonos las correspondientes coverturas
        - como ultimo step de nuestro jobs hemos vuelto a incluir la **actions/upload-artifact@v2**    
                 
                 
                 pytest:
                      name: Unit Testing
                      runs-on: ubuntu-latest
                      steps:
                      - uses: actions/checkout@v2
                      - name: Set up Python
                        uses: actions/setup-python@v2
                        with:
                          python-version: 3.9
                      - name: Install dependencies
                        run: |
                          python -m pip install --upgrade pip
                          pip install -r src/requirements.txt
                      - name: Test with pytest
                        run: |
                          pip install pytest pytest-cov pytest-html pytest-sugar pytest-json-report
                          pytest -v --cov --html=reports/pytest/report.html
                      - name: Archive pytest coverage results
                        uses: actions/upload-artifact@v2
                        with:
                          name: pytest-coverage-report
                          path: reports/pytest/
                      
                      
                      
                      
        

 ### CD-Publish CryptoAPI
  
  * En este caso dicho workflow se ejecutara cuando se haya completado el workflow **CI Python**:

                on:
                  workflow_run:
                    workflows:
                      - "CI Python"
                    branches: [ main ]
                    types:
                      - completed
  
  
  * Los jobs empleados en este workflow:
  
       - **Publish_release**
       
               publish_release:
                 if: ${{ github.event.workflow_run.conclusion == 'success'  }}
                 runs-on: ubuntu-latest
                 steps:
                   # (Optional) GitHub Enterprise requires GHE_HOST variable set
                   #- name: Set GHE_HOST
                   #  run: |
                   #    echo "GHE_HOST=${GITHUB_SERVER_URL##https:\/\/}" >> $GITHUB_ENV

                   # Drafts your next Release notes as Pull Requests are merged into "master"
                   - uses: release-drafter/release-drafter@v5
                     # (Optional) specify config name to use, relative to .github/. Default: release-drafter.yml
                     with:
                       publish: true
                     #   config-name: my-config.yml
                       disable-autolabeler: false
                     env:
                       GITHUB_TOKEN: ${{ secrets.PAT }}
                       
                       
     utilizamos la accion release drafte para generar la release ,una vez agregado a nuestro repositorio , deberemos habilitarlo agregando el archivo de configuracion el cual debe residir en la rama predeterminada **.github/release-drafter.yml**. Puede encontrar documentación al respecto en  [release/drafter](https://github.com/release-drafter/release-drafter) 
     
     
       - **docker_publish**
       
              docker_publish:
                 # REF:  https://docs.github.com/en/actions/publishing-packages/publishing-docker-images
                 name: Build & Publish Image
                 needs: publish_release
                 runs-on: ubuntu-latest
                 steps:
                   - name: Download code
                     uses: actions/checkout@v3

                   - name: Set up QEMU
                     uses: docker/setup-qemu-action@v1

                   - name: Set up Docker Buildx
                     uses: docker/setup-buildx-action@v1

                   - uses: actions-ecosystem/action-get-latest-tag@v1
                     id: get-latest-tag
                   - name: Get the version
                     id: get_version
                     run: |
                       VERSION_TAG=${{ steps.get-latest-tag.outputs.tag }}
                       echo ::set-output name=VERSION::${VERSION_TAG/v/}

                   - name: Log in to the Container registry
                     uses: docker/login-action@f054a8b539a109f9f41c372932f1ae047eff08c9
                     with:
                       registry: ${{ env.REGISTRY }}
                       username: ${{ github.actor }}
                       password: ${{ secrets.PAT }}

                   - name: Login to GHCR
                     run: |
                       echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor}} --password-stdin

                   - name: Build and push into ghcr.io
                     uses: docker/build-push-action@v2
                     id: docker_build
                     with:
                       load: false
                       pull: false
                       push: true    
                       tags: ${{ env.REGISTRY }}/${{ env.REPOSITORY  }}:${{ steps.get_version.outputs.version }}

Los steps de este job serian los siguiente:

   -  Descarga nuestro codigo  de esta forma verificamos nuestro repositorio para que nuestro flujo de trabajo pueda acceder a él.
   -  configuramos tanto QEMU y Docker Buildx para la contruccion de la imagen.
   -  Obtenemos la ultima tag  y con ella extrames y generamos la ultima version correspondiente
   -  Posteriormente nos logeeamos en ghcr.io
   -  Y como ultimo paso realiza la construccion y posterior subida de nuestra imagen versionada al registro correspondiente


 

 
 ## Terraform
 
 Para este workflow comentamos como accion a destacar la siguiente:
 
                - name: Update Pull Request with TF Plan
                  uses: actions/github-script@v6
                  if: github.event.pull_request.merged == false
                  env:
                    PLAN: "terraform\n${{ steps.plan.outputs.stdout }}"
                  with:
                    github-token: ${{ secrets.GITHUB_TOKEN }}
                    script: |
                      const output = `#### Terraform Format and Style 🖌\`${{ steps.fmt.outcome }}\`
                      #### Terraform Initialization ⚙️\`${{ steps.init.outcome }}\`
                      #### Terraform Plan 📖\`${{ steps.plan.outcome }}\`
                      #### Terraform Validation 🤖\`${{ steps.validate.outcome }}\`

                      <details><summary>Show Plan</summary>

                      \`\`\`\n
                      ${process.env.PLAN}
                      \`\`\`

                      </details>

                      *Pushed by: @${{ github.actor }}, Action: \`${{ github.event_name }}\`*`;

                      github.rest.issues.createComment({
                        issue_number: context.issue.number,
                        owner: context.repo.owner,
                        repo: context.repo.repo,
                        body: output
                      })
 
**Actualizar solicitud de extracción** este paso agrega un comentario a la solicitud de extracción con los resultados de los pasos de formato, inicio y planificación. Además, muestra la salida del plan ( steps.plan.outputs.stdout). Esto le permite a su equipo revisar los resultados del plan directamente en el PR en lugar de abrir Terraform Cloud. Este paso solo se ejecuta en solicitudes de incorporación de cambios.Puede encontrar documentacion al repecto en [Doc](https://learn.hashicorp.com/tutorials/terraform/github-actions)

[Volver](https://github.com/KeepCodingCloudDevops5/project-final-devops-leosilva/blob/main/README.md)
