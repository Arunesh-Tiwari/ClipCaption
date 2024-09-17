import os
import subprocess
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Subtitle
from django.http import JsonResponse

def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES['video_file']
        video = Video.objects.create(video_file=video_file, title=video_file.name)
        
        # Extract subtitles using ffmpeg (directly into VTT format)
        video_path = os.path.join(settings.MEDIA_ROOT, video.video_file.name)
        vtt_subtitle_path = os.path.join(settings.MEDIA_ROOT, 'subtitles', f"{os.path.splitext(os.path.basename(video.video_file.name))[0]}.vtt")
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'subtitles'), exist_ok=True)
        
        # ffmpeg command to extract subtitles as WebVTT
        command = f"ffmpeg -i {video_path} -map 0:s:0 {vtt_subtitle_path}"
        subprocess.run(command, shell=True)

        # Read the generated VTT file and store subtitles in the database
        with open(vtt_subtitle_path, 'r') as f:
            subtitles = parse_vtt(f.read())
            for sub in subtitles:
                Subtitle.objects.create(video=video, timestamp=sub['timestamp'], content=sub['content'])
        
        return redirect('video_list')

    return render(request, 'videoapp/upload.html')

# Helper function to parse VTT file
def parse_vtt(vtt_content):
    subtitles = []
    blocks = vtt_content.strip().split('\n\n')
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 2:
            timestamp = lines[0].split(' --> ')[0].strip()  # Start timestamp
            content = ' '.join(lines[1:])
            subtitles.append({'timestamp': timestamp, 'content': content})
    return subtitles

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Generate subtitle file URL (in VTT format)
    subtitle_filename = f"{os.path.splitext(os.path.basename(video.video_file.name))[0]}.vtt"
    subtitle_file_path = os.path.join(settings.MEDIA_ROOT, 'subtitles', subtitle_filename)
    subtitle_file_url = os.path.join(settings.MEDIA_URL, 'subtitles', subtitle_filename)
    
    # Check if the subtitle file exists
    if not os.path.exists(subtitle_file_path):
        subtitle_file_url = None

    # Fetch subtitles for the video and convert timestamp to seconds
    subtitles = Subtitle.objects.filter(video=video)
    subtitle_data = []
    for subtitle in subtitles:
        subtitle_data.append({
            'timestamp': subtitle.timestamp,
            'content': subtitle.content,
            'timestamp_in_seconds': time_string_to_seconds(subtitle.timestamp)
        })

    return render(request, 'videoapp/video_detail.html', {
        'video': video,
        'subtitle_file_url': subtitle_file_url,
        'subtitles': subtitle_data
    })

# Helper function to convert VTT timestamp to seconds
def time_string_to_seconds(time_string):
    parts = time_string.split(':')
    seconds = 0
    if len(parts) == 3:  # Hours:Minutes:Seconds
        seconds += int(parts[0]) * 3600  # Hours to seconds
    if len(parts) >= 2:  # Minutes:Seconds
        seconds += int(parts[-2]) * 60  # Minutes to seconds
        seconds += float(parts[-1])  # Seconds
    return seconds

# Adding search functionality
def search_subtitle(request):
    query = request.GET.get('q')
    video_id = request.GET.get('video_id')
    subtitles = Subtitle.objects.filter(video_id=video_id)

    matches = []
    for subtitle in subtitles:
        if query.lower() in subtitle.content.lower():
            matches.append({
                'timestamp': subtitle.timestamp,
                'content': subtitle.content,
                'timestamp_in_seconds': time_string_to_seconds(subtitle.timestamp)
            })

    return JsonResponse(matches, safe=False)


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videoapp/video_list.html', {'videos': videos})
