# 命令行脚本
命令行基于python click库进行封装开发。所有脚本请放置在bin目录下
## 示例
```python
# simple.py
import click


@click.command(context_settings=dict(ignore_unknown_options=True,
                                     allow_extra_args=True
                                     ))
@click.option("--count", default=1)
@click.option('--name', default="hello world",
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")
```
### 使用
```python
python3 simple.py --count=1 --name=test
```