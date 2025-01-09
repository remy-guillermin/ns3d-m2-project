(define-module (python-fluidsim)
  #:use-module (guix)
  #:use-module ((guix licenses) #:prefix license:)
  #:use-module (guix build-system pyproject)
  #:use-module (guix build-system python)
  #:use-module (guix build utils)
  #:use-module (guix hg-download)
  #:use-module (guix utils)
  #:use-module (common python-packages)
  #:use-module (gnu packages)
  #:use-module (gnu packages mpi)
  #:use-module (gnu packages rust)
  #:use-module (gnu packages rust-apps)
  #:use-module (gnu packages crates-io)
  #:use-module (gnu packages statistics)
  #:use-module (gnu packages bioinformatics)
  #:use-module (gnu packages build-tools)
  #:use-module (gnu packages pkg-config)
  #:use-module (gnu packages python)
  #:use-module (gnu packages python-build)
  #:use-module (gnu packages python-xyz)
  #:use-module (gnu packages python-science)
  #:use-module (common python-fluidfft)
  #:use-module (common python-fluiddyn)
  #:use-module (common python-fluidsim-utils))


;; package python-fluidsim-core
(define-public python-fluidsim-core
  (package
    (name "python-fluidsim-core")
    (version "X.X.X")
    (source
      (origin
        (method hg-fetch)
        (uri
          (hg-reference
            (url "https://foss.heptapod.net/fluiddyn/fluidsim")
            (changeset "34e31ab82a1d")))
        (sha256
          (base32 "0izdby8vp5v2mvszy822k3fis9c0xvkn25y1bb9b1hh7r7cysd0l"))))
    (build-system pyproject-build-system)
    (propagated-inputs (list python-fluiddyn
                             python-importlib-metadata
                      ))
    (arguments '(#:phases (modify-phases %standard-phases
                   ; On patche le HOME
                   (add-before 'build 'patch-HOME-path
                      (lambda _
			(chdir "lib")
                        (setenv "HOME" (getenv "out"))
                        ))
                   ;; On remove la phase de check et de sanity-check
                   (delete 'check)
                   (delete 'sanity-check))))
    (home-page "")
    (synopsis "Framework for studying fluid dynamics with simulations.")
    (description "Framework for studying fluid dynamics with simulations.")
    (license #f)))

;; package python-fluidsim
(define-public python-fluidsim
  (package
    (name "python-fluidsim")
    (version "X.X.X")
    (source
      (origin
        (method hg-fetch)
        (uri
          (hg-reference
            (url "https://foss.heptapod.net/fluiddyn/fluidsim")
            (changeset "34e31ab82a1d")))
        (sha256
          (base32 "0izdby8vp5v2mvszy822k3fis9c0xvkn25y1bb9b1hh7r7cysd0l"))))
    (build-system pyproject-build-system)
    (propagated-inputs (list python-fluidfft
                             python-fluidsim-core
                             python-h5netcdf
                             python-h5py
                             python-ipython
                             python-matplotlib
                             python-mpi4py
                             python-pyfftw
                             python-pymech
                             python-rich
                             python-scipy
                             python-transonic
                             python-xarray
                      ))
    (arguments '(#:phases (modify-phases %standard-phases
                   ; On patche le HOME
                   (add-before 'build 'patch-HOME-path
                      (lambda _
                        (setenv "HOME" (getenv "out"))
                        ))
                   ;; On remove la phase de check et de sanity-check
                   (delete 'check)
                   (delete 'sanity-check))))
    (home-page "")
    (synopsis "Framework for studying fluid dynamics with simulations.")
    (description "Framework for studying fluid dynamics with simulations.")
    (license #f)))

python-fluidsim
