package com.itstar.tzplayer.comm;

import com.itstar.tzplayer.slice.MainAbilitySlice;
import ohos.agp.components.PageSlider;
import ohos.eventhandler.EventHandler;
import ohos.eventhandler.EventRunner;
import ohos.eventhandler.InnerEvent;

public class TZHandler  extends EventHandler {
    private MainAbilitySlice slice;
    private PageSlider banner;
    private int index;
    public TZHandler(EventRunner runner) throws IllegalArgumentException {
        super(runner);
    }

    public TZHandler(EventRunner runner, MainAbilitySlice slice, PageSlider banner) throws IllegalArgumentException {
        super(runner);
        this.slice = slice;
        this.banner = banner;
    }

    @Override
    protected void processEvent(InnerEvent event) {
        super.processEvent(event);
        if (event == null) return;
        switch (event.eventId){
            case 1:
                int max = (int) event.param; //总共有max张图片
                //获取当前banner的图片索引
                int currentPage = banner.getCurrentPage();
                if (currentPage != max-1){
                    index = currentPage+1;
                    //更新图片
                }else{
                    index = 0;
                    //更新图片成一张图片
                }
                slice.getUITaskDispatcher().asyncDispatch(() -> banner.setCurrentPage(index,true));
                break;
            case 2:
                //....
                break;
            default:
                break;
        }
    }
}
