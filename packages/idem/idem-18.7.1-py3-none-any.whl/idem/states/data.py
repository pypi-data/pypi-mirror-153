import json
from pathlib import Path
from typing import Dict

from jinja2 import Template


async def write(
    hub,
    ctx,
    parameters: dict,
    file_name: str = None,
    template: str = None,
    template_file_name: str = None,
) -> Dict[str, Dict]:
    """
    This is a resource that produces output that is recorded in a file.
    If the output file exists it will be overwritten.
    If a jinja template is provided it should accept the "parameters" dictionary and
    the rendered output will be saved to the file.
    Without a Jinja template the output file includes the "parameters" in a json format.
    Jinja template can be passed raw or within a template file

    Sample template:
    {% for resource_name, resource_id in parameters.items() %}
        Created resource: {{ resource_name }} {{ resource_id }}
    {% endfor %}

    Args:
        file_name(Text): The name of the output file with a full path
        parameters(Dict): dictionary of parameters
        template(Text, Optional): Embedded Jinja template within {% raw  %} {% endraw  %}
        template_file_name(Text, Optional): Full path to a jinja template file
            either template or template_file should be specified

    Returns:
        {"result": True|False, "comment": "A message", "old_state": { file_name: content },
        "new_state": { file_name: content }}

    Request Syntax:
        [output-id]:
          data.write:
          - file_name: 'string'
          - template: 'string'
          - parameters: Dict

    Examples:
        .. code-block:: sls

            my-output-file:
                data.write:
                - file_name: "/home/files/OUTPUT.json"
                - template_file_name: "/home/files/template.txt"
                - parameters:
                    resource-test-1.id: ${resource-type:resource-test-1:id}
                    resource-test-1.name: ${resource-type:resource-test-1:name}

            my-output-file:
                data.write:
                - file_name: "/home/files/OUTPUT.json"
                - template: '{% raw  %}
                                {% for resource_name, resource_id in parameters.items() %}
                                    Created resource {{ resource_name }}  {{ resource_id }}
                                {% endfor %}
                            {%  endraw %}'
                - parameters:
                    resource-test-1.id: ${resource-type:resource-test-1:id}
                    resource-test-1.name: ${resource-type:resource-test-1:name}

    """
    result = dict(comment=(), old_state={}, new_state={}, name=file_name, result=True)

    if file_name is None or str(file_name) == 0:
        result["result"] = False
        result["comment"] = ("File name is required.",)
        return result

    if ctx.get("test", False):
        result["comment"] = (f"Would write to file '{file_name}'.",)
        return result

    try:
        # If the output file exists, initialize 'old_state'
        outfile = Path(file_name)
        if outfile.is_file():
            hub.log.debug(
                f"File {file_name} already exists. Its content will be overwritten."
            )
            outfile = open(file_name)
            content = outfile.read()
            if content is not None and len(content) > 0:
                result["old_state"] = {file_name: content}

        output_content = ""
        # Jinja template that accepts a dictionary "parameters"
        if template_file_name is not None:
            template_file = Path(template_file_name)
            if template_file.is_file() is False:
                msg = f"Template file not found: {template_file_name}"
                hub.log.debug(msg)
                result["result"] = False
                result["comment"] = (msg,)
                return result
            else:
                with open(template_file) as curr_template_file:
                    tm = Template(curr_template_file.read())
                    output_content = tm.render(parameters=parameters)
        # Embedded Jinja template
        elif template is not None:
            tm = Template(template)
            output_content = tm.render(parameters=parameters)
        else:
            # No template
            output_content = json.dumps(parameters, indent=4)

        # Writing to the file
        with open(file_name, "w") as outfile:
            outfile.write(output_content)
            outfile.close()

    except FileNotFoundError:
        result["result"] = False
        result["comment"] = (
            f"File(s) not found. File: '{file_name}', template: '{template_file_name}'",
        )
        return result

    result["comment"] = f"Wrote to file '{file_name}'."
    result["new_state"] = {file_name: output_content}
    return result
