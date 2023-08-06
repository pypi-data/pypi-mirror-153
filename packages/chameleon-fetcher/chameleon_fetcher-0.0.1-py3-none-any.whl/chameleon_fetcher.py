from chameleon import PageTemplateLoader


class ChameleonFetcher:

    def __init__(self,
                 template_dir: str,
                 extension: str = None,
                 boolean_attributes: set = None,
                 auto_reload: bool = True,
                 **kwargs):
        """

        :param template_dir: the directory where the templates are located
        :param extension: extension of the template files, defaults to '.pt' - is optional
        :param boolean_attributes: what boolean attributes should be supported, defaults to {'selected', 'checked'} -
        is optional
        :param auto_reload: if the templates should be reloaded on change, defaults to True - is optional
        :param kwargs: other params you want to have available in all templates, e.g. flask=flask - is optional
        """
        if boolean_attributes is None:
            boolean_attributes = {"selected", "checked"}  # why wouldn't you want this?
        if extension is None:
            extension = '.pt'

        self.templates = PageTemplateLoader(template_dir,
                                            extension,
                                            boolean_attributes=boolean_attributes,
                                            auto_reload=auto_reload)
        self.base_kwargs = dict(kwargs)

    def __call__(self, template_name, **kwargs):
        template = self.templates[template_name]
        all_kwargs = dict(self.base_kwargs) | dict(templates=self.templates, template_name=template_name)
        all_kwargs.update(**kwargs)
        return template(**all_kwargs)
