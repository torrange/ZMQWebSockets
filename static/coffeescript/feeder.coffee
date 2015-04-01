feedCreate = (object) ->
	json = JSON.parse(object)
	username = json.username
	avatar = json.avatar
	text = json.text

	html_base = "
		<feed-card>
			<h2>#{username}</h2>
			<img src=\"#{avatar}\">
			<p>#{text}</p>
		</feed-card>"