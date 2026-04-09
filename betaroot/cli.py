"""
BetaRoot CLI
واجهة سطر أوامر احترافية لـ BetaRoot
"""

import click
import json
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from betaroot.core.betaroot import create_betaroot

console = Console()


@click.group()
@click.version_option(version="0.1.0-alpha")
def cli():
    """🌳 BetaRoot - إطار ذكاء اصطناعي رمزي قائم على المنطق الآحادي"""
    pass


@cli.command()
@click.argument("query", nargs=-1, type=click.STRING, required=True)
@click.option("--context", "-c", help="سياق إضافي (JSON)", default=None)
def ask(query, context):
    """طرح سؤال على BetaRoot"""
    question = " ".join(query)
    
    console.print(Panel(f"[bold cyan]السؤال:[/bold cyan] {question}", 
                       title="BetaRoot", border_style="blue"))

    br = create_betaroot()

    # تحميل السياق إذا وُجد
    ctx = {}
    if context:
        try:
            ctx = json.loads(context)
        except json.JSONDecodeError:
            console.print("[red]خطأ: السياق يجب أن يكون JSON صالح[/red]")
            return

    with console.status("[bold green]جاري التفكير حسب مبدأ Only 1...[/bold green]"):
        result = br.process(question, ctx)

    if result.get("success"):
        console.print(Panel(
            result.get("natural_explanation", result.get("answer", "لا يوجد جواب")),
            title="الإجابة والشرح الكامل",
            border_style="green"
        ))
        console.print(f"[dim]الثقة: {result['certainty']*100}% | Only 1, Never 0[/dim]")
    else:
        console.print(Panel(
            f"[red]{result.get('error', 'حدث خطأ')}[/red]\n\n"
            f"التوصية: {result.get('recommendation', 'غير متوفرة')}",
            title="⚠️ تناقض تم اكتشافه",
            border_style="red"
        ))


@cli.command()
@click.option("--facts", is_flag=True, help="عرض إحصائيات قاعدة المعرفة")
@click.option("--system", is_flag=True, help="عرض معلومات النظام")
def info(facts, system):
    """عرض معلومات النظام والذاكرة"""
    br = create_betaroot()

    if system or not facts:
        info = br.system_info()
        console.print(Panel(json.dumps(info, indent=2, ensure_ascii=False), 
                           title="معلومات BetaRoot", border_style="blue"))

    if facts:
        stats = br.memory.stats()
        console.print(Panel(json.dumps(stats, indent=2, ensure_ascii=False), 
                           title="إحصائيات الذاكرة", border_style="magenta"))


@cli.command()
@click.argument("fact", nargs=-1, type=click.STRING)
def add(fact):
    """إضافة حقيقة إلى قاعدة المعرفة"""
    if not fact:
        console.print("[red]يجب إدخال الحقيقة[/red]")
        return

    fact_text = " ".join(fact)
    br = create_betaroot()
    fact_id = br.add_fact(fact_text)

    console.print(f"[green]✓ تمت إضافة الحقيقة بنجاح[/green]")
    console.print(f"معرف الحقيقة: [cyan]{fact_id}[/cyan]")


@cli.command()
def test():
    """تشغيل الاختبارات بسرعة"""
    import subprocess
    console.print("[bold yellow]جاري تشغيل الاختبارات...[/bold yellow]")
    result = subprocess.run(["pytest", "tests/", "-q", "--tb=no"], capture_output=True, text=True)
    console.print(result.stdout)
    if result.returncode == 0:
        console.print("[bold green]✓ تم اجتياز جميع الاختبارات بنجاح[/bold green]")
    else:
        console.print("[bold red]✗ فشل بعض الاختبارات[/bold red]")


if __name__ == "__main__":
    cli()
