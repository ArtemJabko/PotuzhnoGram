package app.exteraless.settings;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.media.AudioAttributes;
import android.media.SoundPool;
import android.os.SystemClock;
import android.view.MotionEvent;
import android.view.View;
import android.view.HapticFeedbackConstants;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import java.util.Locale;

/** An offline joke, not a radiation sensor. Uses media volume and no permissions. */
public class PotuzhnoMeterActivity extends BaseFragment {
    private MeterView meter;
    @Override public View createView(Context context) {
        actionBar.setTitle("ПотужноМетр");
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setBackgroundColor(0xff09182b);
        actionBar.setTitleColor(0xfff4f8ff);
        actionBar.setItemsColor(0xfff4f8ff, false);
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override public void onItemClick(int id) { if (id == -1) finishFragment(); }
        });
        if (meter != null) meter.dispose();
        meter = new MeterView(context);
        fragmentView = meter;
        return fragmentView;
    }
    @Override public void onPause() {
        if (meter != null) meter.suspend();
        super.onPause();
    }
    @Override public void onFragmentDestroy() {
        if (meter != null) meter.dispose();
        super.onFragmentDestroy();
    }

    private static final class MeterView extends View {
        private static final int BG=0xff09182b, CARD=0xff122b46, WHITE=0xfff4f8ff;
        private static final int YELLOW=0xffffd43b, BLUE=0xff47b4ff, MUTED=0xffb0c4da;
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final RectF rect = new RectF();
        private SoundPool audio;
        private int tickSound, boomSound, tickStream, boomStream;
        private boolean tickReady, boomReady, holding, broken, muted;
        private float progress;
        private long lastFrame, nextTick;
        private int pointer = -1;
        private float scale=1, ox, oy;
        private final Runnable frame = new Runnable() {
            @Override public void run() {
                if (!holding) return;
                long now=SystemClock.uptimeMillis();
                progress=Math.min(1f, progress+Math.min(100,now-lastFrame)/6500f);
                lastFrame=now;
                if (progress>=1f) {
                    holding=false; broken=true; updateDescription();
                    if (audio!=null && tickStream!=0) audio.stop(tickStream);
                    if (!muted && boomReady && audio!=null)
                        boomStream=audio.play(boomSound,.45f,.45f,2,0,1f);
                    performHapticFeedback(HapticFeedbackConstants.LONG_PRESS);
                    announceForAccessibility("Ваш потужнометр не витримав рівня потужності у повітрі");
                } else {
                    if (now>=nextTick) {
                        if (!muted && tickReady && audio!=null)
                            tickStream=audio.play(tickSound,.28f,.28f,1,0,1f);
                        nextTick=now+(long)(360-325*progress);
                    }
                    postOnAnimation(this);
                }
                invalidate();
            }
        };
        MeterView(Context context) {
            super(context);
            setFocusable(true); setClickable(true);
            updateDescription();
            audio=new SoundPool.Builder().setMaxStreams(3).setAudioAttributes(
                new AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_GAME)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION).build()).build();
            audio.setOnLoadCompleteListener((pool,id,status)-> {
                if(status==0) { if(id==tickSound) tickReady=true; if(id==boomSound) boomReady=true; }
            });
            tickSound=audio.load(context,R.raw.potuzno_tick,1);
            boomSound=audio.load(context,R.raw.potuzno_boom,1);
        }
        private void updateDescription() {
            setContentDescription(broken ? "ПотужноМетр зламано. Натисніть, щоб повторити." :
                "ПотужноМетр — жартівливий симулятор. Утримуйте екран для вимірювання. Подвійний дотик із TalkBack запускає або зупиняє шкалу.");
        }
        private void begin() {
            if (broken || holding) return;
            holding=true; lastFrame=SystemClock.uptimeMillis(); nextTick=lastFrame;
            postOnAnimation(frame); invalidate();
        }
        private void stop() { holding=false; removeCallbacks(frame); invalidate(); }
        private void silence() {
            if (audio != null) {
                audio.autoPause();
                if (tickStream != 0) audio.stop(tickStream);
                if (boomStream != 0) audio.stop(boomStream);
                tickStream = boomStream = 0;
            }
        }
        void suspend() {
            stop(); pointer=-1;
            silence();
        }
        void dispose() {
            suspend();
            if(audio!=null) { audio.release(); audio=null; }
        }
        @Override protected void onDetachedFromWindow() { suspend(); super.onDetachedFromWindow(); }
        private void reset() {
            stop(); progress=0; broken=false;
            silence();
            updateDescription(); invalidate();
        }
        @Override public boolean performClick() {
            super.performClick();
            if(broken) reset(); else if(holding) stop(); else begin();
            return true;
        }
        @Override public boolean onTouchEvent(MotionEvent e) {
            float x=(e.getX()-ox)/scale, y=(e.getY()-oy)/scale;
            switch(e.getActionMasked()) {
                case MotionEvent.ACTION_DOWN:
                    if(x>268 && y<50) {
                        muted=!muted;
                        if(muted) silence();
                        announceForAccessibility(muted ? "Звук вимкнено" : "Звук увімкнено");
                        invalidate(); return true;
                    }
                    if(broken) { reset(); return true; }
                    pointer=e.getPointerId(0); begin(); return true;
                case MotionEvent.ACTION_UP:
                case MotionEvent.ACTION_CANCEL:
                    stop(); pointer=-1; return true;
                case MotionEvent.ACTION_POINTER_UP:
                    if(e.getPointerId(e.getActionIndex())==pointer) { stop(); pointer=-1; }
                    return true;
                default: return true;
            }
        }
        private void text(Canvas c,String s,float x,float y,float size,int color,boolean bold) {
            paint.setStyle(Paint.Style.FILL); paint.setColor(color); paint.setTextSize(size);
            paint.setTypeface(bold ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT);
            paint.setTextAlign(Paint.Align.CENTER); c.drawText(s,x,y,paint);
        }
        private void box(Canvas c,float l,float t,float r,float b,int color,float radius) {
            paint.setStyle(Paint.Style.FILL);paint.setColor(color);rect.set(l,t,r,b);
            c.drawRoundRect(rect,radius,radius,paint);
        }
        @Override protected void onDraw(Canvas c) {
            super.onDraw(c); c.drawColor(BG);
            // Fit the entire instrument in portrait, landscape and small windows.
            scale=Math.min(getWidth()/360f,getHeight()/590f);
            ox=(getWidth()-360*scale)/2; oy=(getHeight()-590*scale)/2;
            c.save();c.translate(ox,oy);c.scale(scale,scale);
            text(c,"ПОЛЬОВА ЛАБОРАТОРІЯ",132,29,11,MUTED,true);
            box(c,272,5,348,45,CARD,16);
            text(c,muted?"ЗВУК: НІ":"ЗВУК: ТАК",310,29,10,WHITE,true);
            text(c,broken?"ПЕРЕВАНТАЖЕННЯ":"РІВЕНЬ ПОТУЖНОСТІ",180,84,20,broken?YELLOW:WHITE,true);
            text(c,broken?"Прилад пішов у легенди":"Перевір, наскільки потужно навколо",180,108,12,MUTED,false);
            box(c,20,135,340,433,CARD,28);
            paint.setStyle(Paint.Style.STROKE);paint.setStrokeWidth(16);paint.setStrokeCap(Paint.Cap.ROUND);
            rect.set(74,167,286,379);paint.setColor(0xff23415f);c.drawArc(rect,140,260,false,paint);
            paint.setColor(broken?0xffff8860:YELLOW);c.drawArc(rect,140,Math.max(.1f,260*progress),false,paint);
            paint.setStrokeWidth(2);paint.setColor(0xff365675);
            for(int i=0;i<=26;i++) {
                double a=Math.toRadians(140+i*10);
                c.drawLine(180+(float)Math.cos(a)*120,273+(float)Math.sin(a)*120,
                    180+(float)Math.cos(a)*(i%5==0?130:125),273+(float)Math.sin(a)*(i%5==0?130:125),paint);
            }
            text(c,broken?"BOOM":String.format(Locale.US,"%03d",Math.round(progress*100)),180,285,broken?43:62,WHITE,true);
            text(c,broken?"100 / 100":"ПОТУЖ / 100",180,313,12,MUTED,true);
            text(c,broken?"✕ СЕНСОР НЕ ВИТРИМАВ":holding?"● СКАНУВАННЯ":"● ГОТОВИЙ ДО ВИМІРЮВАННЯ",180,409,11,holding?YELLOW:BLUE,true);
            box(c,20,450,340,532,broken?0xff49342c:CARD,20);
            if(broken) {
                text(c,"Ваш потужнометр не витримав",180,480,15,WHITE,true);
                text(c,"рівня потужності у повітрі",180,504,15,WHITE,true);
            } else {
                text(c,holding?"ТРИМАЙ. ПОТУЖНІСТЬ ЗРОСТАЄ.":"УТРИМУЙ ЕКРАН",180,482,14,WHITE,true);
                text(c,holding?"Відпусти, щоб зупинити":"Клацання ставатиме частішим",180,506,12,MUTED,false);
            }
            text(c,broken?"ТОРКНИСЬ, ЩОБ ПОВТОРИТИ":"Жартівливий симулятор · не справжній дозиметр",180,564,11,broken?YELLOW:MUTED,false);
            c.restore();
        }
    }
}
