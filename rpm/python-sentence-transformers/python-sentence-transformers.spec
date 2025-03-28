Name:           python-sentence-transformers
Version:        4.0.1
Release:        1%{?dist}
Summary:        Compute embeddings, retrieval, and reranking to train models
License:        Apache-2.0
URL:            https://www.SBERT.net
Source:         %{pypi_source sentence_transformers}
BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
This framework provides an easy method to compute embeddings for accessing,
using, and training state-of-the-art embedding and reranker models. It
computes embeddings using Sentence Transformer models or calculates
similarity scores using Cross-Encoder (a.k.a. reranker) models. This
unlocks a wide range of applications, including semantic search, semantic
textual similarity, and paraphrase mining.}

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
* Thu Mar 27, 2025 -- Al Stone <ahs3@fedoraproject.org> -- 4.0.1-1
- Initial packaging
