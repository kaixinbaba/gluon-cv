max_time = 120
stage("Sanity Check") {
  node {
    ws('workspace/gluon-cv-lint') {
      timeout(time: max_time, unit: 'MINUTES') {
        checkout scm
        sh """#!/bin/bash
        set -e
        conda env update -n gluon-cv-lint -f tests/pylint.yml --prune
        conda activate gluon-cv-lint
        conda list
        make clean
        make pylint
        """
      }
    }
  }
}

stage("Unit Test") {
  parallel 'Mxnet': {
    node('linux-gpu') {
      ws('workspace/gluon-cv-py3-mxnet') {
        timeout(time: max_time, unit: 'MINUTES') {
          checkout scm
          VISIBLE_GPU=env.EXECUTOR_NUMBER.toInteger() % 8
          sh """#!/bin/bash
          conda env remove -n gluon-cv-py3-mxnet_test -y
          set -ex
          # remove and create new env instead
          conda env create -n gluon-cv-py3-mxnet_test -f tests/py3_mxnet.yml
          conda env update -n gluon-cv-py3-mxnet_test -f tests/py3_mxnet.yml --prune
          conda activate gluon-cv-py3-mxnet_test
          conda list
          export CUDA_VISIBLE_DEVICES=${VISIBLE_GPU}
          export KMP_DUPLICATE_LIB_OK=TRUE
          make clean
          # from https://stackoverflow.com/questions/19548957/can-i-force-pip-to-reinstall-the-current-version
          pip install --upgrade --force-reinstall --no-deps .
          env
          export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64
          export MPLBACKEND=Agg
          export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
          nosetests --with-timer --timer-ok 5 --timer-warning 20 -x --with-coverage --cover-package gluoncv -v tests/unittests
          nosetests --with-timer --timer-ok 5 --timer-warning 20 -x --with-coverage --cover-package gluoncv -v tests/model_zoo
          rm -f coverage.svg
          coverage-badge -o coverage.svg
          if [[ ${env.BRANCH_NAME} == master ]]; then
              aws s3 cp coverage.svg s3://gluon-cv.mxnet.io/coverage.svg --acl public-read --cache-control no-cache
              echo "Uploaded coverage badge to http://gluon-cv.mxnet.io"
          else
              aws s3 cp coverage.svg s3://gluon-vision-staging/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/coverage.svg --acl public-read --cache-control no-cache
              echo "Uploaded coverage badge to http://gluon-vision-staging.s3-website-us-west-2.amazonaws.com/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/coverage.svg"
          fi
          """
        }
      }
    }
  },
  'Torch': {
    node('linux-gpu') {
      ws('workspace/gluon-cv-py3-torch') {
        timeout(time: max_time, unit: 'MINUTES') {
          checkout scm
          VISIBLE_GPU=env.EXECUTOR_NUMBER.toInteger() % 8
          sh """#!/bin/bash
          conda env remove -n gluon-cv-py3-torch_test -y
          set -ex
          # remove and create new env instead
          conda env create -n gluon-cv-py3-torch_test -f tests/py3_torch.yml
          conda env update -n gluon-cv-py3-torch_test -f tests/py3_torch.yml --prune
          conda activate gluon-cv-py3-torch_test
          conda list
          export CUDA_VISIBLE_DEVICES=${VISIBLE_GPU}
          export KMP_DUPLICATE_LIB_OK=TRUE
          make clean
          # from https://stackoverflow.com/questions/19548957/can-i-force-pip-to-reinstall-the-current-version
          pip install --upgrade --force-reinstall --no-deps .
          env
          export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64
          export MPLBACKEND=Agg
          export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
          nosetests --with-timer --timer-ok 5 --timer-warning 20 -x --with-coverage --cover-package gluoncv/torch -v tests/model_zoo_torch
          """
        }
      }
    }
  },
  'Auto': {
    node('linux-gpu') {
      ws('workspace/gluon-cv-py3-auto') {
        timeout(time: max_time, unit: 'MINUTES') {
          checkout scm
          VISIBLE_GPU=env.EXECUTOR_NUMBER.toInteger() % 8
          sh """#!/bin/bash
          conda env remove -n gluon-cv-py3-auto_test -y
          set -ex
          # remove and create new env instead
          conda env create -n gluon-cv-py3-auto_test -f tests/py3_auto.yml
          conda env update -n gluon-cv-py3-auto_test -f tests/py3_auto.yml --prune
          conda activate gluon-cv-py3-auto_test
          conda list
          export CUDA_VISIBLE_DEVICES=${VISIBLE_GPU}
          export KMP_DUPLICATE_LIB_OK=TRUE
          make clean
          # from https://stackoverflow.com/questions/19548957/can-i-force-pip-to-reinstall-the-current-version
          pip install --upgrade --force-reinstall --no-deps .
          env
          export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64
          export MPLBACKEND=Agg
          export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
          nosetests --with-timer --timer-ok 60 --timer-warning 120 -x --with-coverage --cover-package gluoncv -v tests/auto
          """
        }
      }
    }
  }
}


stage("Build Docs") {
  node('linux-gpu') {
    ws('workspace/gluon-cv-docs') {
      timeout(time: max_time, unit: 'MINUTES') {
        checkout scm
        VISIBLE_GPU=env.EXECUTOR_NUMBER.toInteger() % 8
        sh """#!/bin/bash
        conda env remove -n gluon_vision_docs -y
        set -ex
        conda env create -n gluon_vision_docs -f docs/build.yml
        conda env update -n gluon_vision_docs -f docs/build.yml --prune
        conda activate gluon_vision_docs
        export PYTHONPATH=\${PWD}
        export CUDA_VISIBLE_DEVICES=${VISIBLE_GPU}
        env
        export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64
        git submodule update --init --recursive
        git clean -fx
        cd docs && make clean && make html
        sed -i.bak 's/33\\,150\\,243/23\\,141\\,201/g' build/html/_static/material-design-lite-1.3.0/material.blue-deep_orange.min.css;
        sed -i.bak 's/2196f3/178dc9/g' build/html/_static/sphinx_materialdesign_theme.css;
        sed -i.bak 's/pre{padding:1rem;margin:1.5rem\\s0;overflow:auto;overflow-y:hidden}/pre{padding:1rem;margin:1.5rem 0;overflow:auto;overflow-y:scroll}/g' build/html/_static/sphinx_materialdesign_theme.css
        if [[ ${env.BRANCH_NAME} == master ]]; then
            aws s3 cp s3://gluon-cv.mxnet.io/coverage.svg build/html/coverage.svg
            aws s3 sync --delete build/html/ s3://gluon-cv.mxnet.io/ --acl public-read --cache-control max-age=7200
            aws s3 cp build/html/coverage.svg s3://gluon-cv.mxnet.io/coverage.svg --acl public-read --cache-control max-age=300
            echo "Uploaded doc to http://gluon-cv.mxnet.io"
        else
            aws s3 cp s3://gluon-vision-staging/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/coverage.svg build/html/coverage.svg
            aws s3 sync --delete build/html/ s3://gluon-vision-staging/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/ --acl public-read
            echo "Uploaded doc to http://gluon-vision-staging.s3-website-us-west-2.amazonaws.com/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/index.html"
        fi
        """

        if (env.BRANCH_NAME.startsWith("PR-")) {
          pullRequest.comment("Job ${env.BRANCH_NAME}-${env.BUILD_NUMBER} is done. \nDocs are uploaded to http://gluon-vision-staging.s3-website-us-west-2.amazonaws.com/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/index.html \nCode coverage of this PR: ![pr.svg](http://gluon-vision-staging.s3-website-us-west-2.amazonaws.com/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/coverage.svg?) vs. Master: ![master.svg](http://gluon-cv.mxnet.io/coverage.svg?)")
        }
      }
    }
  }
}
