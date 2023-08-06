# Installing TuxRun via RPM packages

TuxRun provides RPM packages that have minimal dependencies, and should work
on any RPM-based (Fedora, etc) system.

1) Create `/etc/yum.repos.d/tuxrun.repo` with the following contents:

```
[tuxrun]
name=tuxrun
type=rpm-md
baseurl=https://tuxrun.org/packages/
gpgcheck=1
gpgkey=https://tuxrun.org/packages/repodata/repomd.xml.key
enabled=1

```

2) Install tuxrun as you would any other package:

```
# dnf install tuxrun
```

Upgrades will be available in the same repository, so you can get them using
the same procedure you already use to get other updates for your system.
