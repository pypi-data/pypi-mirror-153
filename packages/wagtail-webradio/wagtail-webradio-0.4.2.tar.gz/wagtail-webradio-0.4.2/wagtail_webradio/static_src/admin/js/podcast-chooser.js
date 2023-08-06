import $ from 'jquery';

function createPodcastChooser(id) {
  const $chooser = $('#' + id + '-chooser');
  const $title = $chooser.find('.title');
  const $input = $('#' + id);
  const $editLink = $chooser.find('.edit-link');
  const chooserBaseUrl = $chooser.data('chooserUrl');

  /*
  Construct initial state of the chooser from the rendered (static) HTML and
  arguments passed to createPodcastChooser. State is either null (= no podcast
  chosen) or a dict of id, title and edit_link.

  The result returned from the podcast chooser modal (see
  wagtail_webradio.views.chooser.podcast_chosen) is a superset of this, and can
  therefore be passed directly to chooser.setState.
  */
  let state = null;
  if ($input.val()) {
    state = {
      id: $input.val(),
      edit_link: $editLink.attr('href'),
      title: $title.text(),
    };
  }

  /* Define public API functions for the chooser */
  const chooser = {
    getState: () => state,
    getValue: () => state && state.id,
    setState(newState) {
      if (newState) {
        $input.val(newState.id);
        $title.text(newState.title);
        $chooser.removeClass('blank');
        $editLink.attr('href', newState.edit_link);
      } else {
        $input.val('');
        $chooser.addClass('blank');
      }

      state = newState;
    },
    getTextLabel(opts) {
      if (!state) return null;
      const result = state.title;
      if (opts && opts.maxLength && result.length > opts.maxLength) {
        return result.substring(0, opts.maxLength - 1) + '…';
      }

      return result;
    },
    focus() {
      $('.action-choose', $chooser).focus();
    },
    openChooserModal() {
      /* global ModalWorkflow, PODCAST_CHOOSER_MODAL_ONLOAD_HANDLERS */
      ModalWorkflow({
        url: chooserBaseUrl,
        onload: PODCAST_CHOOSER_MODAL_ONLOAD_HANDLERS,
        responses: {
          podcastChosen(result) {
            chooser.setState(result);
          },
        },
      });
    },

    clear() {
      chooser.setState(null);
    },
  };

  $('.action-choose', $chooser).on('click', () => {
    chooser.openChooserModal();
  });

  $('.action-clear', $chooser).on('click', () => {
    chooser.clear();
  });

  return chooser;
}

window.createPodcastChooser = createPodcastChooser;
