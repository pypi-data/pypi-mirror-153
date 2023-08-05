buildsets.yaml: buildsets.py
	python3 buildsets.py > buildsets.yaml

test:
	tuxsuite build-set --git-repo 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git' --git-ref master --tux-config buildsets.yaml --set-name tinyconfigs
