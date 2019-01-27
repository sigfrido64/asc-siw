"""
Con questo script posso vedere le variabili che vengono mandate via con il Form quando premo il relativo pulsante.

<script type="text/javascript">
$('form').submit(function() {
  alert($(this).serialize());
  return false;
});
</script>


"""
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa

__all__ = ['celery_app']
