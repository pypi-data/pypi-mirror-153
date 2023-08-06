# **Welcome to Optumi 👋**

### Description

Optumi is a cloud service that makes it easy for data scientists to develop & train ML models on powerful computing resources.

We offer a JupyterLab extension that runs local Python notebooks in the cloud. We offer access to a wide variety of powerful cloud resources to launch interactive sessions or batch jobs.

### Installation

To install from PyPI:

- Make sure you have Python installed (3.7 or later)
- Open a terminal
- Install the extension by running ```pip install -U jupyterlab-optumi```
- Launch JupyterLab by running ```jupyter lab```

That’s it! You can now click the ![Optumi](https://www.optumi.com/wp-content/uploads/2020/10/cropped-optumi-logo-o-32x32.png) icon in the left sidebar to open the extension.

For more information about Optumi, please visit our [knowledge base](https://optumi.notion.site/optumi/Optumi-Knowledge-Base-f51e2040569b46449601851c91caea29).

### Notes

If you are running JupyterLab from an anaconda environment, you’ll need to run the install command with that environment activated. You can do this by launching JupyterLab, selecting File -> New -> Terminal and running the install command there. If you do this, you will need to shut down and restart Jupyterlab before using the extension.

If you already have the extension installed outside of an anaconda environment and want to reinstall it inside of an anaconda environment, you will need to add the ```-U``` flag to the pip install command.

Safari browser is not supported.

If for any reason the extension is not a good fit for your needs, you can uninstall it by running ```pip uninstall jupyterlab-optumi```. We will of course be sad to see you go!

### TroubleShooting

Test the install by running ```jupyter lab extension list``` and ```jupyter server extension list```. You should see jupyterlab_optumi in both outputs.

If you do not see jupyterlab_optumi in both outputs, run ```jupyter server extension enable jupyterlab_optumi –user``` and test the install again.

### Questions

If you have any questions, please reach out to the Optumi team. You can contact us by emailing cs@optumi.com or through our website www.optumi.com.

