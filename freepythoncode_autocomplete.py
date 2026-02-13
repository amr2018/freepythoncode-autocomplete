
import sublime
import sublime_plugin
import os
import sys

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
            
           
            user_home = os.environ.get('USERPROFILE') or os.path.expanduser("~")
            
            external_paths = [
                os.path.join(user_home, r"AppData\Local\Programs\Python\Python313\Lib\site-packages"),
                os.path.join(user_home, r"AppData\Local\Programs\Python\Python313\Lib")
            ]

            code = view.substr(sublime.Region(0, view.size()))
            row, col = view.rowcol(locations[0])
            
           
            script = jedi.Script(code, path=view.file_name() or 'untitled.py')
            
            completions = script.complete(row + 1, col)
            
            if not completions:
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
