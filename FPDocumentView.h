/* FPDocumentView */

#import <Cocoa/Cocoa.h>
#import <PDFKit/PDFKit.h>

@class FPGraphic;
@class MyDocument;

#define FPSelectionChangedNotification @"FPSelectionChangedNotification"

@interface FPDocumentView : NSView
{
    IBOutlet MyDocument *_doc;
    PDFDocument *_pdf_document;
    NSUInteger _current_page;
    PDFDisplayBox _box;
    float _scale_factor;
    BOOL _draws_shadow;
    BOOL _inQuickMove;
    BOOL _is_printing;

    NSMutableArray *_overlayGraphics;
    NSMutableSet *_selectedGraphics;
    FPGraphic *_editingGraphic;
    
    // For zooming
    IBOutlet NSScrollView *_scrollView;
}

- (void)setPDFDocument:(PDFDocument *)pdf_document;

- (void)zoomIn:(id)sender;
- (void)zoomOut:(id)sender;

- (void)nextPage;
- (void)previousPage;
- (void)scrollToPage:(NSUInteger)page;

- (float)scaleFactor;

- (BOOL)shouldEnterQuickMove;
- (void)beginQuickMove:(id)unused;
- (void)endQuickMove:(id)unused;

- (NSSet *)selectedGraphics;
- (void)deleteSelectedGraphics;

- (BOOL)handleColorChange:(NSColor*)newColor;
- (NSColor*)defaultStrokeColor;

- (NSUInteger)getViewingMidpointToPage:(NSUInteger *)page pagePoint:(NSPoint*)pagePoint;
- (void)scrollToMidpointOnPage:(NSUInteger)page point:(NSPoint)midPoint;

// place image
- (IBAction)placeImage:(id)sender;

// coordinate transforms
- (NSUInteger)pageForPointFromEvent:(NSEvent *)theEvent;
- (NSUInteger)pageForPoint:(NSPoint)point;
- (NSPoint)pagePointForPointFromEvent:(NSEvent *)theEvent
                                 page:(NSUInteger)page;
- (NSRect)convertRect:(NSRect)rect toPage:(NSUInteger)page;
- (NSRect)convertRect:(NSRect)rect fromPage:(NSUInteger)page;
- (NSPoint)convertPoint:(NSPoint)point toPage:(NSUInteger)page;
- (NSPoint)convertPoint:(NSPoint)point fromPage:(NSUInteger)page;

// printing
- (FPDocumentView *)printableCopy;
- (NSRect)rectForPage:(int)page; // indexed from 1, not 0

// opening and saving
- (NSArray *)archivalOverlayGraphics;
- (void)setOverlayGraphicsFromArray:(NSArray *)arr;

// font
- (NSFont *)currentFont;

// private
- (NSAffineTransform *)transformForPage:(NSUInteger)page;
@end
