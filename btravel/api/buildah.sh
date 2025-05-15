buildah from --name btrvl-bld docker.io/elixir:1.18-otp-27

buildah copy btrvl-bld src /app
buildah config --workingdir /app btrvl-bld

buildah run btrvl-bld mix local.hex --force
buildah run btrvl-bld mix local.rebar --force

buildah run btrvl-bld mix deps.get
buildah run btrvl-bld mix compile

buildah config --env PORT=4001 btrvl-bld

buildah config --cmd '["mix", "phx.server"]' btrvl-bld

buildah commit btrvl-bld btrvl-api:latest