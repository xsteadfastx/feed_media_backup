.PHONY: init clean docker-build

init:
	pipenv --three
	pipenv install --dev

clean:
	rm -rf *.pyc
	rm -rf .cache
	rm -rf .mypy_cache
	rm -rf .tox
	rm -rf __pycache__
	rm -rf build

docker-build: clean
	docker build -t feed_media_backup .
