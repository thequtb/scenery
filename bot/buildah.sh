buildah from --name tg-bld docker.io/library/python:3.13-slim
buildah copy tg-bld src /app
buildah config --workingdir /app tg-bld

buildah run tg-bld pip install --upgrade pip
buildah run tg-bld pip install -r requirements.txt
buildah config --cmd '["python", "-m", "bot"]' tg-bld
buildah commit tg-bld tg-bld:latest

