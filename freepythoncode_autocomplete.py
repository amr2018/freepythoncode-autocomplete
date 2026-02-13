import sublime
import sublime_plugin
import os
import sys

# 1. إعداد مسارات المكتبات المدمجة (Jedi/Parso)
plugin_path = os.path.dirname(os.path.realpath(__file__))
libs_path = os.path.join(plugin_path, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

class FreepythoncodeAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.python"):
            return None
            
        try:
            import jedi
            
            # 2. المسار الذي وجدته أنت (نحقنه يدوياً في قائمة المسارات)
            # سنضيف المسار الرئيسي ومسار الـ site-packages
            external_paths = [
                r"C:\Users\Hp\AppData\Local\Programs\Python\Python313\Lib\site-packages",
                r"C:\Users\Hp\AppData\Local\Programs\Python\Python313\Lib"
            ]

            code = view.substr(sublime.Region(0, view.size()))
            row, col = view.rowcol(locations[0])
            
            # 3. إنشاء السكريبت مع إخبار Jedi بالبحث في المسارات الخارجية
            # نستخدم sys_path هنا لإضافة مسارات Python 3.13
            script = jedi.Script(code, path=view.file_name() or 'untitled.py')
            
            # ندمج المسارات في عملية البحث
            completions = script.complete(row + 1, col)
            
            # إذا لم يجد نتائج، سنحاول مرة أخرى مع إجبار المسارات (طريقة بديلة)
            if not completions:
                # محاولة متقدمة بإضافة المسارات لـ sys.path مؤقتاً لـ Jedi
                for p in external_paths:
                    if p not in sys.path:
                        sys.path.append(p)
                script = jedi.Script(code, path=view.file_name() or 'untitled.py')
                completions = script.complete(row + 1, col)

            items = []
            for c in completions:
                items.append(sublime.CompletionItem(
                    trigger=c.name,
                    annotation=f"{c.type} (v3.13)",
                    completion=c.name,
                    kind=sublime.KIND_FUNCTION if c.type == "function" else sublime.KIND_VARIABLE
                ))
            
            return (items, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
            
        except Exception as e:
            print(f"FreePythonCode Error: {e}")
            return None
