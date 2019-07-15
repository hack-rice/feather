from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

template = env.get_template("accept.html")

output = template.render(title="Hello!", first_name="Hugh")

if __name__ == "__main__":
    print(output)
