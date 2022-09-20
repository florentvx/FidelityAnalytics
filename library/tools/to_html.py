import jinja2

def template_to_html(my_dictionary, output_html_path, template_name = "my_template.jinja"):

    jfsl = jinja2.FileSystemLoader(searchpath="./library/template/")
    tmp_env = jinja2.Environment(loader=jfsl)
    template = tmp_env.get_template(template_name)
    output = template.render(my_dictionary)
    with open(output_html_path, "w") as text_file:
        text_file.write(output)