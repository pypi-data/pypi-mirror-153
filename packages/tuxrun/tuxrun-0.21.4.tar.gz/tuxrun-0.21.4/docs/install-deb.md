# Installing TuxRun via Debian packages

TuxRun provides Debian packages that have minimal dependencies, and should
work on any Debian or Debian-based (Ubuntu, etc) system.

1) Download the [repository signing key](https://tuxrun.org/packages/signing-key.gpg)
and save it to `/etc/apt/trusted.gpg.d/tuxrun.gpg`.

```
# wget -O /etc/apt/trusted.gpg.d/tuxrun.gpg \
  https://tuxrun.org/packages/signing-key.gpg
```

2) Create /etc/apt/sources.list.d/tuxrun.list with the following contents:

```
deb https://tuxrun.org/packages/ ./
```

3) Install `tuxrun` as you would any other package:

```
# apt update
# apt install tuxrun
```

Upgrading tuxrun will work just like it would for any other package (`apt
update`, `apt upgrade`).
