# detection-fake-news-ml
Detection fake news using ML

# Crear flujo para el scrapper (https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-scheduled-function)
1. Crear azure function
2. Crear trigger

## Useful commands
# remove pip packages
pip freeze | xargs pip uninstall -y
# activate conda
conda activate 'env'
# create env.yml
conda env export > env.yml
# create requirements
pip freeze > requirements.txt
# install pip packages
pip install -r requirements.txt 

## Create docker and resources
# Create the docker and test it
docker build --tag python-docker .
docker images
docker run python-docker

# Create the container in azure and login in, and deploy
docker push tfmtrainmodel.azurecr.io/tfm-train-model:v1

# create task to run the container
az acr task create --name tfmtraintask --registry tfmtrainmodel --cmd tfmtrainmodel.azurecr.io/tfm-train-model:latest --schedule "0 4 * */1 *" --context /dev/null

# task list
az acr task timer list \ 
    --name tfmtimertask \
    --registry tfmtrainmodel.azurecr.io

# remove task
az acr task timer remove \
  --name tfmtimertask \
  --registry tfmtrainmodel.azurecr.io