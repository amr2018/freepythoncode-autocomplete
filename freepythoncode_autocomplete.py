import sublime
import sublime_plugin
import sys
import os

# 1. تحديد مسار مجلد libs الموجود داخل إضافة FreePythonCode
plugin_path = os.path.dirname(os.path.realpath(__file__))
libs_path = os.path.join(plugin_path, 'libs')

# 2. إضافة المسار إلى sys.path لكي يتمكن Sublime من رؤية Jedi
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

class FreepythoncodeAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.python"):
            return None
            
        try:
            # سيتم استيراد jedi الآن من مجلد libs المحلي
            import jedi
            
            code = view.substr(sublime.Region(0, view.size()))
            row, col = view.rowcol(locations[0])
            
            script = jedi.Script(code, path=view.file_name() or 'untitled.py')
            completions = script.complete(row + 1, col)
            
            items = []
            for c in completions:
                items.append(sublime.CompletionItem(
                    trigger=c.name,
                    annotation=c.type,
                    completion=c.name,
                    kind=sublime.KIND_FUNCTION if c.type == "function" else sublime.KIND_VARIABLE
                ))
            
            return (items, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
            
        except Exception as e:
            print("FreePythonCode Error:", e)
            return None