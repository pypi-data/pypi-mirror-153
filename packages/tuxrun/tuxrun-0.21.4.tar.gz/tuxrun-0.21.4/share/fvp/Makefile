RUNTIME ?= "podman"

.PHONE: build

build: fvp fvp-aemva fvp-morello

fvp: Dockerfile
	$(RUNTIME) build --tag tuxrun:fvp .

fvp-aemva: aemva/Dockerfile
	cd aemva && $(RUNTIME) build --tag fvp:aemva-11.17.21 .

fvp-morello: morello/Dockerfile
	cd morello && $(RUNTIME) build --tag fvp:morello-0.11.33 .

clean:
	$(RUNTIME) image rm tuxrun:fvp fvp:aemva-11.17.21 fvp:morello-0.11.33
