package com.itstar.tzplayer.slice;

import com.itstar.tzplayer.Bean.SongItem;
import com.itstar.tzplayer.ResourceTable;
import com.itstar.tzplayer.comm.SongScanner;
import com.itstar.tzplayer.provider.SongListProvider;
import ohos.aafwk.ability.AbilitySlice;
import ohos.aafwk.ability.DataAbilityHelper;
import ohos.aafwk.ability.DataAbilityRemoteException;
import ohos.aafwk.content.Intent;
import ohos.agp.components.Component;
import ohos.agp.components.Image;
import ohos.agp.components.ListContainer;
import ohos.agp.utils.LayoutAlignment;
import ohos.agp.window.dialog.ToastDialog;
import ohos.agp.window.service.WindowManager;
import ohos.data.resultset.ResultSet;
import ohos.media.photokit.metadata.AVStorage;

import java.text.SimpleDateFormat;
import java.util.ArrayList;

public class LoadAbilitySlice extends AbilitySlice {
    private DataAbilityHelper helper;
    private ArrayList<SongItem> songs;
    private ListContainer listContainer;
    @Override
    public void onStart(Intent intent) {
        super.onStart(intent);
        super.setUIContent(ResourceTable.Layout_ability_load);
        getWindow().addFlags(WindowManager.LayoutConfig.MARK_TRANSLUCENT_STATUS);
        helper = DataAbilityHelper.creator(this);
        scan_songs();
    }

    private void scan_songs() {
        Image load_btn = (Image) findComponentById(ResourceTable.Id_load_button);
        load_btn.setClickedListener(component -> {
            //扫描指定目录音频
            SongScanner.scan_sd(this);
            //查询扫描到的音频数据
            try {
                ResultSet resultSet = helper.query(AVStorage.Audio.Media.EXTERNAL_DATA_ABILITY_URI, null, null);
                songs = new ArrayList<>();
                if (resultSet == null || resultSet.getRowCount() == 0){
                    new ToastDialog(this).setText("未扫描到歌曲").setAlignment(LayoutAlignment.CENTER).show();
                }
                while(resultSet.goToNextRow()){
                    SongItem songItem = new SongItem();
                    songItem.setSong_id(resultSet.getInt(resultSet.getColumnIndexForName(AVStorage.AVBaseColumns.ID)));//歌曲ID
                    songItem.setSong_name(resultSet.getString(resultSet.getColumnIndexForName(AVStorage.AVBaseColumns.TITLE)));//音乐的名称
                    songItem.setSinger(resultSet.getString(resultSet.getColumnIndexForName("artist")));//歌手名
                    songItem.setDuration(new SimpleDateFormat("mm:ss").format(resultSet.getColumnIndexForName(AVStorage.AVBaseColumns.DURATION)));
                    songItem.setData(resultSet.getString(resultSet.getColumnIndexForName(AVStorage.AVBaseColumns.DATA)));//音频地址
                    songs.add(songItem);
                }
                show_songs();
            } catch (DataAbilityRemoteException e) {
                e.printStackTrace();
            }
        });
    }

    private void show_songs() {
        listContainer = (ListContainer) findComponentById(ResourceTable.Id_load_list_container);
        SongListProvider songListProvider = new SongListProvider(songs, this);
        listContainer.setItemProvider(songListProvider);
    }

    @Override
    public void onActive() {
        super.onActive();
    }

    @Override
    public void onForeground(Intent intent) {
        super.onForeground(intent);
    }
}
