package com.itstar.tzplayer.provider;

import com.itstar.tzplayer.Bean.SongItem;
import com.itstar.tzplayer.ResourceTable;
import com.itstar.tzplayer.slice.LoadAbilitySlice;
import ohos.agp.components.*;
import ohos.global.icu.util.Freezable;

import java.util.List;

public class SongListProvider extends BaseItemProvider {
    private List<SongItem> list;
    private LoadAbilitySlice slice;

    public SongListProvider(List<SongItem> list,LoadAbilitySlice slice) {
        this.list = list;
        this.slice =slice;
    }

    @Override
    public int getCount() {
        return list == null?0:list.size();
    }

    @Override
    public Object getItem(int position) {
        if (list !=null && position>=0 && position<list.size()){
            return list.get(position);
        }
        return null;
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public Component getComponent(int position, Component convertComponent, ComponentContainer componentContainer) {
        final Component cpt;
        if (convertComponent == null) {
            cpt = LayoutScatter.getInstance(slice).parse(ResourceTable.Layout_songs_list, null, false);
        } else {
            cpt = convertComponent;
        }
        SongItem item = list.get(position);
        //设置歌手封面
        Image song_image = (Image) cpt.findComponentById(ResourceTable.Id_song_image);
        song_image.setCornerRadius(40);
        if (item.getPhoto_resource() !=0){
            song_image.setPixelMap(item.getPhoto_resource());
        }
        //设置歌曲名，歌手名·
        Text song_name = (Text) cpt.findComponentById(ResourceTable.Id_song_name);
        Text song_singer = (Text) cpt.findComponentById(ResourceTable.Id_song_singer);
        song_name.setText(item.getSong_name());
        song_singer.setText(item.getSinger());

        return cpt;
    }
}
