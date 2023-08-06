class PodcastChooser {
  constructor(html, idPattern) {
    this.html = html;
    this.idPattern = idPattern;
  }

  render(placeholder, name, id, initialState) {
    const html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
    placeholder.outerHTML = html;
    /* global createPodcastChooser */
    const chooser = createPodcastChooser(id);
    chooser.setState(initialState);
    return chooser;
  }
}

window.telepath.register(
  'wagtail_webradio.widgets.PodcastChooser',
  PodcastChooser
);
