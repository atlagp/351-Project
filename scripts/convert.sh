find "annarborsamples" | grep "mp3" | while read -r file; do
		base="${file%%.*}"
		echo "$base.mp3"
		echo "$base.wav"
		ffmpeg -nostdin -i "$base.mp3" -map_metadata 0 -loglevel error -stats "$base.wav" 
done
