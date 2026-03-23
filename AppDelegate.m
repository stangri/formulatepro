//
//  AppDelegate.m
//  FormulatePro
//
//  Created by Andrew de los Reyes on 7/5/06.
//  Copyright 2006 Andrew de los Reyes. All rights reserved.
//

#import "AppDelegate.h"

@implementation AppDelegate

- (BOOL)applicationShouldOpenUntitledFile:(NSApplication *)application
{
    return NO;
}

- (IBAction)showLicense:(id)sender
{
    NSString *path = [[NSBundle mainBundle] pathForResource:@"LICENSE" ofType:@"txt"];
    NSError *error = nil;
    NSString *license = [NSString stringWithContentsOfFile:path encoding:NSUTF8StringEncoding error:&error];
    if (!license) return;

    NSWindow *window = [[NSWindow alloc] initWithContentRect:NSMakeRect(0, 0, 500, 400)
                                                   styleMask:(NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable)
                                                     backing:NSBackingStoreBuffered
                                                       defer:NO];
    [window setTitle:@"License"];
    [window center];

    NSScrollView *scrollView = [[NSScrollView alloc] initWithFrame:[[window contentView] bounds]];
    [scrollView setAutoresizingMask:(NSViewWidthSizable | NSViewHeightSizable)];
    [scrollView setHasVerticalScroller:YES];

    NSTextView *textView = [[NSTextView alloc] initWithFrame:[[scrollView contentView] bounds]];
    [textView setEditable:NO];
    [textView setFont:[NSFont userFixedPitchFontOfSize:11]];
    [textView setAutoresizingMask:(NSViewWidthSizable | NSViewHeightSizable)];
    [[textView textStorage] beginEditing];
    [[textView textStorage] setAttributedString:[[NSAttributedString alloc] initWithString:license]];
    [[textView textStorage] endEditing];

    [scrollView setDocumentView:textView];
    [window setContentView:scrollView];
    [window setReleasedWhenClosed:NO];
    [window makeKeyAndOrderFront:nil];
}

- (IBAction)provideFeedback:(id)sender
{
    [[NSWorkspace sharedWorkspace] openURL:
        [NSURL URLWithString:@"mailto:formulate@adlr.info"]];
}

- (IBAction)viewBugList:(id)sender
{
    [[NSWorkspace sharedWorkspace] openURL:
        [NSURL
         URLWithString:@"http://code.google.com/p/formulatepro/issues/list"]];
}

- (IBAction)fileNewBug:(id)sender
{
    [[NSWorkspace sharedWorkspace] openURL:
     [NSURL
      URLWithString:@"http://code.google.com/p/formulatepro/issues/entry"]];
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    /* // this code copies the arrow cursor image to the clipboard
    NSImage *arrow;
    int i;
    NSData *d;
    NSPasteboard *pb;
    
    [arrowToolButton setImage:[[NSCursor arrowCursor] image]];
    arrow = [[NSCursor arrowCursor] image];
    DLog(@"reps %d\n", i, [[arrow representations] count]);
    d = [[arrow bestRepresentationForDevice:nil]
        representationUsingType:NSTIFFFileType
                     properties:nil];
    DLog(@"d = %x\n", d);
    pb = [NSPasteboard generalPasteboard];
    [pb declareTypes:[NSArray arrayWithObject:NSTIFFPboardType] owner:nil];
    DLog(@"ok? %d\n", [pb setData:d forType:NSTIFFPboardType]);*/
}

@end
