# ML6 kfp-components

This is a package for reusable kubeflow pipelines components.

We consider reusable components to be so general that they can be used
in any pipeline without further customization. 

For the purposes of this repository, we distinguish three kinds of components:
- lightweight (python function) components
- custom image (python function) components
- yaml based components

An example for each type of component can be found under `ml6_kfp_components/examples`.

Lightweight components are simple python function components which are
built on public base images (possibly with minor additional installed packages).

Custom image components are python function components with more custom dependencies.
We create a custom container image and host it in a publicly accessible Google Artifact Registry repository.

Yaml based components are the most general framework. 
Your component can be based on any programming language and can be arbitrarily complex.
Just package your component as a container image and define an interface using a yaml file.

In this package, we not only define these components, but also preload them, 
so that users can easily use the components by just installing this package and
importing the components they want to use.