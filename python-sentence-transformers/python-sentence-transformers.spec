Name:           python-sentence-transformers
Version:        4.0.1
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Embeddings, Retrieval, and Reranking

# No license information obtained, it's up to the packager to fill it in
License:        ...
URL:            https://www.SBERT.net
Source:         %{pypi_source sentence_transformers}

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'sentence-transformers' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-sentence-transformers
Summary:        %{summary}

%description -n python3-sentence-transformers %_description

# For official Fedora packages, review which extras should be actually packaged
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#Extras
%pyproject_extras_subpkg -n python3-sentence-transformers dev,onnx,onnx-gpu,openvino,train


%prep
%autosetup -p1 -n sentence_transformers-%{version}


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires -x dev,onnx,onnx-gpu,openvino,train


%build
%pyproject_wheel


%install
%pyproject_install
# Add top-level Python module names here as arguments, you can use globs
%pyproject_save_files -l ...


%check
%pyproject_check_import


%files -n python3-sentence-transformers -f %{pyproject_files}


%changelog
%autochangelog