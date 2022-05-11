package com.itstar.tzplayer.Bean;

import java.util.Objects;

public class SongItem {
    //歌曲的id号
    private int song_id;
    //歌曲名
    private String song_name;
    //歌手名
    private String singer;
    //写真的url地址值
    private String photo_url = "";
    //写真的resource值
    private int photo_resource = 0;
    //歌曲资源地址
    private String data;
    //歌曲时长
    private String duration;

    public SongItem(int song_id, String song_name, String singer, String photo_url, int photo_resource, String data, String duration) {
        this.song_id = song_id;
        this.song_name = song_name;
        this.singer = singer;
        this.photo_url = photo_url;
        this.photo_resource = photo_resource;
        this.data = data;
        this.duration = duration;
    }

    public SongItem() {
    }

    public int getSong_id() {
        return song_id;
    }

    public void setSong_id(int song_id) {
        this.song_id = song_id;
    }

    public String getSong_name() {
        return song_name;
    }

    public void setSong_name(String song_name) {
        this.song_name = song_name;
    }

    public String getSinger() {
        return singer;
    }

    public void setSinger(String singer) {
        this.singer = singer;
    }

    public String getPhoto_url() {
        return photo_url;
    }

    public void setPhoto_url(String photo_url) {
        this.photo_url = photo_url;
    }

    public int getPhoto_resource() {
        return photo_resource;
    }

    public void setPhoto_resource(int photo_resource) {
        this.photo_resource = photo_resource;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public String getDuration() {
        return duration;
    }

    public void setDuration(String duration) {
        this.duration = duration;
    }

    @Override
    public String toString() {
        return "SongItem{" +
                "song_id=" + song_id +
                ", song_name='" + song_name + '\'' +
                ", singer='" + singer + '\'' +
                ", photo_url='" + photo_url + '\'' +
                ", photo_resource=" + photo_resource +
                ", data='" + data + '\'' +
                ", duration='" + duration + '\'' +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        SongItem songItem = (SongItem) o;
        return Objects.equals(song_name, songItem.song_name) && Objects.equals(singer, songItem.singer);
    }

    @Override
    public int hashCode() {
        return Objects.hash(song_name, singer);
    }
}
